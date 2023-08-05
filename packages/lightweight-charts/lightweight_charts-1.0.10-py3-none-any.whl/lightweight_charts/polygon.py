import asyncio
import threading
from queue import Queue
import pandas as pd
import datetime as dt
import re
import json
try:
    import requests
    import websockets
except ImportError:
    pass


class PolygonAPI:
    def __init__(self, chart):
        self._chart = chart
        self._lasts = {}
        self._key = None
        self._using_live_data = False

        self._ws = None
        self._send_q = Queue()
        self._q = Queue()
        self.lock = threading.Lock()

    def api_key(self, key): self._key = key

    def stock(self, symbol: str, timeframe: str, start_date: str, end_date='now', live: bool = False):
        """
        Requests and displays stock data pulled from Polygon.io.\n
        :param symbol:      Ticker to request.
        :param timeframe:   Timeframe to request (1min, 5min, 2H, 1D, 1W, 2M, etc).
        :param start_date:  Start date of the data (YYYY-MM-DD).
        :param end_date:    End date of the data (YYYY-MM-DD). If left blank, this will be set to today.
        :param live:        If true, the data will be updated in real-time.
        """
        self._set('stock', symbol, timeframe, start_date, end_date, live)

    def option(self, symbol, strike, expiration, timeframe, start_date, end_date='now', live=False):
        pass

    def forex(self, fiat_pair, timeframe, start_date, end_date='now', live=False):
        pass

    def crypto(self, symbol, fiat, timeframe, start_date, end_date='now', live=False):
        pass

    def _set(self, sec_tyoe, ticker, timeframe, start_date, end_date, live):

        end_date = dt.datetime.now().strftime('%Y-%m-%d') if end_date == 'now' else end_date
        multiplier, timespan = _convert_timeframe(timeframe)
        try:
            response = requests.get(f'''
                https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{start_date}/{end_date}?apiKey={self._key}''')
        except NameError:
            raise ImportError('The "requests" library must be installed to use the polygon method.')
        if response.status_code != 200:
            print(f'Polygon.io request failed (Error code {response.status_code})')
            return pd.DataFrame()
        data = response.json()['results']
        df = pd.DataFrame(data)
        df.rename(columns={'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume'},
                  inplace=True)
        df['date'] = pd.to_datetime(df['t'], unit='ms')
        self._lasts[data['ticker']] = {
            'time': df['date'].iloc[-1],
            'price': df['close'].iloc[-1],
            'volume': df['volume'].iloc[-1],
        }

        self._chart.set(df)
        if not live:
            return
        self._using_live_data = True
        self._start_thread(self._key)
        self._send_q.put(('_subscribe', f'Q.{ticker}'))
        self._send_q.put(('_subscribe', f'AM.{ticker}')) if self._chart._volume_enabled else None

    def _start_thread(self, key):
        with self.lock:
            if not self._ws:
                threading.Thread(target=asyncio.run, args=[self._websocket_connect(key)], daemon=True).start()

    async def _subscribe(self, ticker):
        await self._send('subscribe', ticker)

    async def _handle_tick(self, data):
        symbol = data['sym']

        if data['ev'] == 'Q':
            self._lasts[symbol]['time'] = pd.to_datetime(data['t'], unit='ms')
            self._lasts[symbol]['price'] = (data['bp']+data['ap'])/2

        elif data['ev'] == 'A':
            self._lasts[symbol]['volume'] += data['v']   # TODO this wont work. You need to keep track of the timeframe and calculate it

        self._q.put((self._chart.update_from_tick, pd.Series(self._lasts[symbol])))

    async def _websocket_connect(self, key):
        try:
            async with websockets.connect('wss://delayed.polygon.io/stocks', ssl=False) as ws:
                with self.lock:
                    self._ws = ws
                await self._send('auth', key)
                asyncio.create_task(self._thread_loop())
                while 1:
                    response = await ws.recv()
                    print(response)
                    data = json.loads(response)
                    if data['ev'] == 'Q':
                        await self._handle_tick(data)
        except NameError:
            raise ImportError('The "websockets" library must be installed to pull live data from polygon.io.')

    async def _thread_loop(self):
        while 1:
            value = self._send_q.get_nowait()
            if not value:
                await asyncio.sleep(0.1)
                continue
            func, args = value
            await func(*args)
        # self._ws = None

    async def _send(self, action, params):
        if not self._ws:
            await asyncio.sleep(0.1)
        await self._ws.send(json.dumps({'action': action, 'params': params}))


def _convert_timeframe(timeframe):
    spans = {
        'min': 'minute',
        'H': 'hour',
        'D': 'day',
        'W': 'week',
        'M': 'month',
    }
    try:
        multiplier = re.findall(r'\d+', timeframe)[0]
    except IndexError:
        return 1, timeframe
    timespan = spans[timeframe.replace(multiplier, '')]
    return multiplier, timespan

# goes in chart.py
    # def _polygon_loop(self):
    #     while not self._exit.is_set():
    #         try:
    #             val = self.polygon._q.get_nowait()
    #         except queue.Empty:
    #             time.sleep(0.05)
    #             continue
    #         func, arg = val
    #         func(arg)

