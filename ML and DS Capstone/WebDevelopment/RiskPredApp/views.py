from django.shortcuts import render

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
#from .forms import *
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import (View,TemplateView,
ListView,DetailView,
CreateView,DeleteView,
UpdateView)
from . import models
from .forms import *
from django.core.files.storage import FileSystemStorage

import pandas as pd
import numpy as np
import pickle
import yfinance as yf


class dataUploadView(View):
    form_class = riskPredForm
    success_url = reverse_lazy('success')
    template_name = 'create.html'
    failure_url= reverse_lazy('fail')
    filenot_url= reverse_lazy('filenot')
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    def post(self, request, *args, **kwargs):
        #print('inside post')
        form = self.form_class(request.POST, request.FILES)
        #print('inside form')
        if form.is_valid():
            form.save()
            inp_stk= request.POST.get('Stock')
           
            
            def data_collect(stkname, start_date, end_date):

                all_data = []

                df = yf.download(stkname, start=start_date, end=end_date, 
                                multi_level_index=False, auto_adjust=True, progress=False)

                stock = yf.Ticker(stkname)
                
                if not df.empty:
                    df["Stock"] = stkname.replace(".NS", "")
                    df['Sector'] = stock.info.get('sector')
                    df['Industry'] = stock.info.get('industry')
                    df['Market Cap'] = stock.info.get('marketCap')
                    df['Dividend Yield'] = stock.info.get('trailingAnnualDividendYield')
                    df['Dividend Rate'] = stock.info.get('trailingAnnualDividendRate')
                    df['PE Ratios'] = stock.info.get('trailingPE')
                    df['ROE Values'] = stock.info.get('netIncomeToCommon') / (stock.info.get('bookValue') * stock.info.get('sharesOutstanding'))

                    df.reset_index(inplace=True)   # Move Date from index to column
                    all_data.append(df)

                stocks_df = pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()

                latest_year = pd.to_datetime(end_date).year
                three_years = [latest_year-2, latest_year-1, latest_year]
                df_3y = stocks_df[stocks_df['Date'].dt.year.isin(three_years)]
                # Find stocks with data in all 3 years
                stocks_full_3y = (
                    df_3y.groupby('Stock')['Date'].apply(lambda x: x.dt.year.nunique())
                    .loc[lambda count: count == 3]
                    .index
                )

                # Filter DataFrame to only those stocks
                df_3y_full = df_3y[df_3y['Stock'].isin(stocks_full_3y)]

                return df_3y_full

            
            def calc_metrics(stocks_df, nifty_df):
                feature_rows = []
                stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])

                nifty_returns = nifty_df[['Date', 'Close']].copy()
                nifty_df['Date'] = pd.to_datetime(nifty_df['Date'])
                nifty_returns = nifty_df[['Date','Close']].set_index('Date')['Close'].pct_change().dropna()
                
                # stocks_df.groupby('Stock').apply(calc_metrics, include_groups=False).reset_index()
                for stk, stk_data in stocks_df.groupby('Stock'): 

                    sector = stk_data['Sector'].unique()[0]  # use [0] instead of .item() for robustness
                    industry = stk_data['Industry'].unique()[0]
                    market_cap = stk_data['Market Cap'].unique()[0]
                    
                    stk_data = stk_data.sort_values('Date')
                    stk_data['daily_return'] = stk_data['Close'].pct_change()
                    avg_daily_return = stk_data['daily_return'].mean()
                    std_daily = stk_data['daily_return'].std()
                    trading_days = stk_data['Date'].dt.date.nunique()  # number of trading days in this period
                    
                    annualized_return = (1 + avg_daily_return) ** trading_days - 1
                    annualized_volatility = std_daily * np.sqrt(trading_days)
                    risk_free_rate = 0.05  # (0.05 or 5% annual for INR/India government bonds)
                    sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility if annualized_volatility != 0 else np.nan
                    max_drawdown = ((stk_data['Close'].cummax() - stk_data['Close']) / stk_data['Close'].cummax()).max()
                    avg_volume = stk_data['Volume'].mean()
                    volume_spike_pct = (stk_data['Volume'] > 2 * avg_volume).mean()
                    
                    # Market relationship: Use group directly instead of 'year_data'
                    nifty_data = nifty_df.set_index('Date').sort_index()
                    daily_returns = nifty_data['Close'].pct_change().dropna()
                    # nifty_returns already covers the whole period, match dates
                    nifty_year = nifty_returns.loc[daily_returns.index.min(): daily_returns.index.max()]
                    combined = pd.DataFrame({
                        'Stock_Return': daily_returns,
                        'NIFTY_Return': nifty_year
                    }).dropna()
                    
                    if len(combined) > 30:  # require at least 30 days
                        cov_matrix = np.cov(combined['Stock_Return'], combined['NIFTY_Return'])
                        beta = cov_matrix[0,1] / cov_matrix[1,1] if cov_matrix[1,1] != 0 else np.nan
                        corr_nifty = combined['Stock_Return'].corr(combined['NIFTY_Return'])
                    else:
                        beta = np.nan
                        corr_nifty = np.nan

                    feature_row = {
                        'Stock': stk,
                        'Sector': sector,   
                        'Industry': industry,
                        'MarketCap': market_cap,
                        'Annualized_Return': annualized_return,
                        'Annualized_Volatility': annualized_volatility,
                        'Sharpe_Ratio': sharpe_ratio,
                        'Max_Drawdown': max_drawdown*100, # Percentage
                        'Avg_Volume': avg_volume,
                        'Volume_Spike_Pct': volume_spike_pct*100,  # Percentage
                        'Beta_vs_NIFTY': beta,
                        'Corr_with_NIFTY': corr_nifty
                    }
                
                    feature_rows.append(feature_row)
                
                features_df = pd.DataFrame(feature_rows)

                return features_df
            

            stkname = inp_stk.strip().upper() + '.NS'

            start_date = "2022-01-01"
            end_date   = "2024-12-31"

            nifty_df = pd.read_csv('NIFTY50.csv')
            stocks_df = data_collect(stkname, start_date, end_date)
            features_df = calc_metrics(stocks_df, nifty_df)

            scale_model=pickle.load(open("scaler.pkl",'rb'))
            loaded_model=pickle.load(open('best_model.sav','rb'))

            input_cols = ['MarketCap', 'Annualized_Return',
                'Annualized_Volatility', 'Max_Drawdown', 'Avg_Volume',
                'Volume_Spike_Pct', 'Beta_vs_NIFTY', 'Corr_with_NIFTY']
            scaled_input=scale_model.fit_transform(features_df[input_cols])

            scaled_df = pd.DataFrame(scaled_input, columns=input_cols)
            scaled_df[['Stock', 'Sector', 'Industry']] = features_df[['Stock', 'Sector', 'Industry']]

            # Results
            result = loaded_model.predict(scaled_input)  # Take the first value

            if result == 0:
                res_stk = 'Balanced Stock'
            elif result == 1:
                res_stk = 'Aggressive Stock'
            else:
                res_stk = 'Conservative Stock'

            stock = scaled_df['Stock'].iloc[0]
            industry = scaled_df['Industry'].iloc[0]
            sector = scaled_df['Sector'].iloc[0]

            final_output ={'stock':stock,'industry':industry,'sector':sector,'res_stk':res_stk}

            return render(request, "succ_msg.html", final_output)


        else:
            return redirect(self.failure_url)