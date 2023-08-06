import numpy as np
import math as math

def rsi(prices, period):
    """
    Calculate the RSI values.

    This function helps you to calculate RSI values for your desired
    prices and timeperiod.
    
    The RSI (Relative Strength Index) is a technical indicator used in
    financial analysis to measure the magnitude and velocity of price
    movements.

    Parameters
    ----------
    prices : numpy.ndarray
        Numpy array of type float containing an assets pricehistory.
    period : int
        Number of timeperiods used for the calculation.

    Returns
    -------
    rsi (numpy.ndarray) : Numpy array of type float containing the RSI values calculated.
    """
    delta = np.diff(prices)
    gain = delta.copy()
    loss = delta.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    
    avg_gain = np.zeros(len(prices))
    avg_loss = np.zeros(len(prices))

    rs = np.zeros(len(prices))
    rsi = np.zeros(len(prices))

    avg_gain[period] = np.mean(gain[:period])
    avg_loss[period] = np.abs(np.mean(loss[:period]))
    
    for i in range(period + 1, len(prices)):
        avg_gain[i] = (avg_gain[i-1] * (period - 1) + gain[i-1]) / period
        avg_loss[i] = (avg_loss[i-1] * (period - 1) + np.abs(loss[i-1])) / period
        rs[i] = avg_gain[i] / avg_loss[i]
        rsi[i] = 100 - (100 / (1 + rs[i]))
    
    return rsi

def ma(prices, period):
    """
    Calculate the MA values.

    This function helps you to calculate MA values for your desired
    prices and timeperiod.

    The simple moving average (MA) is a commonly used technical
    analysis tool in finance. It is a calculation that helps smooth
    out price data over a specified period of time, providing a
    clearer picture of the underlying trend.
    
    Parameters
    ----------
    prices : numpy.ndarray
        Numpy array of type float containing an assets pricehistory.
    period : int
        Number of timeperiods used for the calculation.

    Returns
    -------
    ma (numpy.ndarray) : Numpy array of type float containing the MA values calculated.
    """
    ma = np.convolve(prices, np.ones(period), mode='valid') / period

    return ma

def smma(prices, period):
    """
    Calculate the SMMA values.

    This function helps you to calculate SMMA values for your desired
    prices and timeperiod.
    
    SMMA stands for the Smoothed Moving Average. It is a variation of
    the simple moving average (MA) that applies additional smoothing
    to the price data.

    Parameters
    ----------
    prices : numpy.ndarray
        Numpy array of type float containing an assets pricehistory.
    period : int
        Number of timeperiods used for the calculation.

    Returns
    -------
    smma (numpy.ndarray) : Numpy array of type float containing the SMA values calculated.
    """
    smma = np.zeros(len(prices))
    smma[period - 1] = ma(prices, period)[-1]

    for i in range(period, len(prices)):
        smma[i] = (smma[i - 1] * (period - 1) + prices[i]) / period

    return smma

def ema(prices, period):
    """
    Calculate the EMA values.

    This function helps you to calculate EMA values for your desired
    prices and timeperiod.

    EMA stands for Exponential Moving Average. It is another type of
    moving average commonly used in technical analysis to analyze
    price trends and generate trading signals. The EMA gives more
    weight to recent prices, making it more responsive to recent price
    changes compared to the simple moving average (MA) and smoothed
    moving average (SMMA).

    Parameters
    ----------
    prices : numpy.ndarray
        Numpy array of type float containing an assets pricehistory.
    period : int
        Number of timeperiods used for the calculation.

    Returns
    -------
    ema (numpy.ndarray) : Numpy array of type float containing the EMA values calculated.
    """
    ema = np.zeros(len(prices))
    ema[period-1] = ma(prices, period)[-1]
    multiplier = 2 / (period + 1)
    
    for i in range(period, len(prices)):
        ema[i] = (prices[i] - ema[i-1]) * multiplier + ema[i-1]
    
    return ema

def macd(prices, fast_period, slow_period, signal_period): 
    """
    Calculate the MACD values.

    This function helps you to calculate MACD values for your desired
    prices and timeperiods.

    MACD stands for Moving Average Convergence Divergence. It is a
    popular technical analysis indicator used to identify potential
    trend reversals, generate buy and sell signals, and gauge the
    strength of a trend. The MACD consists of two lines, the MACD
    line and the signal line, as well as a histogram.
    
    Parameters
    ----------
    prices : numpy.ndarray  
        Numpy array of type float containing an assets pricehistory.
    fast_period : int
        Number of timeperiods used for the fast length calculation.
    slow_period : int
        Number of timeperiods used for the slow length calculation.
    signal_period : int
        Number of timeperiods used for the signal calculation.

    Returns
    -------
    hist (numpy.ndarray) : Numpy array of type float containing the histogram values calculated.
    macd (numpy.ndarray) : Numpy array of type float containing the MACD values calculated.
    signal (numpy.ndarray) : Numpy array of type float containing the signal values calculated.
    """
    fast = ema(prices, fast_period)
    slow = ema(prices, slow_period)

    macd = fast - slow

    signal = ema(macd, signal_period)

    hist = macd - signal

    return hist, macd, signal

def bollinger_bands(prices, period, standard_deviation):
    """
    Calculate the Bollinger Bands values.

    This function helps you to calculate BB values for your desired
    prices, timeperiod and standard deviation.

    Bollinger Bands is a widely used technical analysis tool developed by
    John Bollinger. It consists of three lines plotted on a price chart:
    a middle band, an upper band, and a lower band. Bollinger Bands are
    designed to provide a visual representation of price volatility and
    potential price levels where the price is likely to revert or reverse.
    
    Parameters
    ----------
    prices : numpy.ndarray
        Numpy array of type float containing an assets pricehistory.
    period : int
        Number of timeperiods used for the calculation.
    standard_deviation : int
        Number used as standard deviation within the calculation.

    Returns
    -------
    middle (numpy.ndarray) : Numpy array of type float containing the middle BB values calculated.
    upper (numpy.ndarray) : Numpy array of type float containing the upper BB values calculated.
    lower (numpy.ndarray) : Numpy array of type float containing the lower BB values calculated.
    """
    middle = ma(prices, period)

    std = np.zeros(len(middle))
    upper = np.zeros(len(middle))
    lower = np.zeros(len(middle))

    std = np.std(np.lib.stride_tricks.sliding_window_view(prices, period), axis=1)

    for i in range(len(middle)):
        upper[i] = (middle[i] + (standard_deviation * std[i]))
        lower[i] = (middle[i] - (standard_deviation * std[i]))

    return middle, upper, lower

def fibonacci_retracement(high, low, levels, uptrend):
    """
    Calculate the Fibonacci Retracement level values.

    This function helps you to calculate fibonacci retracement levle values for
    your desired prices and levels.
    
    Fibonacci retracement is a technical analysis tool used to identify potential
    levels of support and resistance in a price chart. It is based on the
    Fibonacci sequence, a mathematical sequence in which each number is the sum
    of the two preceding numbers.

    Parameters
    ----------
    high : float
        This is the highest price reached by your asset within your choosen momentum.
    low : float
        This is the lowest price reached by your asset within your choosen momentum.
    levels : numpy.ndarray
        Numpy array of type float containing the level values you want to be calculated.
    uptrend : boolean
        Defines if you are in an uptrend(True) or in a downtrend(False)

    Returns
    -------
    retracement_levels (numpy.ndarray) : Numpy array of type float containing the retracement level values calculated.
    """
    diff = high - low
    retracement_levels = np.zeros(len(levels))

    for i in range(len(levels)):
        if(uptrend):
            retracement_levels[i] = high - (diff * levels[i])
        else:
            retracement_levels[i] = low + (diff * levels[i])

    return retracement_levels

def fibonacci_extension(high, low, levels, uptrend):
    """
    Calculate the Fibonacci Extension level values.

    This function helps you to calculate fibonacci extension levle values for
    your desired prices and levels.

    Fibonacci extension is a technical analysis tool that is used to project
    potential price targets or levels beyond the current price trend. It is
    an extension of the Fibonacci retracement tool and uses the same Fibonacci
    ratios.
    
    Parameters
    ----------
    high : float
        This is the highest price reached by your asset within your choosen momentum.
    low : float
        This is the lowest price reached by your asset within your choosen momentum.
    levels : numpy.ndarray
        Numpy array of type float containing the level values you want to be calculated.
    uptrend : boolean
        Defines if you are in an uptrend(True) or in a downtrend(False)

    Returns
    -------
    extension_levels (numpy.ndarray) : Numpy array of type float containing the extension level values calculated.
    """
    diff = high - low
    extension_levels = np.zeros(len(levels))

    for i in range(len(levels)):
        if(uptrend):
            extension_levels[i] = high + (diff * levels[i])
        else:
            extension_levels[i] = low - (diff * levels[i])

    return extension_levels