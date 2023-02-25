import requests
import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
from datetime import datetime

def get_station_list():
    url = "https://www.neverin.hr/postaja/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    station_list = []
    
    for table_header in soup.find_all("th"):
        if table_header.find("a"):
            name = table_header.find("a").text
            lat = float(table_header.find_next("td").text.replace(u'\N{DEGREE SIGN}', ""))
            lon = float(table_header.find_next("td").find_next("td").text.replace(u'\N{DEGREE SIGN}', ""))
            station_list.append((name, lat, lon))  
            
    return station_list

def get_station_data(station_name):
    url = f"https://api.neverin.hr/v2/stations/?station={station_name.replace(' ', '-')}"
    response = requests.get(url)
    data = response.json()
    
    if 'error' in data:
        return None
        
    return data

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather Data App")
        self.geometry("800x600")
        
        self.station_list = get_station_list()
        self.selected_station_name = tk.StringVar(value=self.station_list[0][0])
        self.selected_station_lat = tk.StringVar(value=self.station_list[0][1])
        self.selected_station_lon = tk.StringVar(value=self.station_list[0][2])
        
        self.station_dropdown = tk.OptionMenu(self, self.selected_station_name, *[station[0] for station in self.station_list])
        self.station_dropdown.pack(pady=10)
        
        self.show_data_button = tk.Button(self, text="Show Data", command=self.show_data)
        self.show_data_button.pack()
        
        self.result_frame = ttk.Frame(self)
        self.result_canvas = tk.Canvas(self.result_frame)
        self.scrollbar = ttk.Scrollbar(self.result_frame, orient=tk.VERTICAL, command=self.result_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.result_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.result_canvas.configure(
                scrollregion=self.result_canvas.bbox("all")
            )
        )
        
        self.result_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.result_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.result_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.result_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def show_data(self):
        station_name = self.selected_station_name.get()
        station_data = get_station_data(station_name)        
    
        try:
            daily_data = station_data['data']['archive']['daily']

            datetime_list = [datetime.utcfromtimestamp(date) for date in daily_data['datetime'][-7:]]
            tempL_list = [round(temp, 1) for temp in daily_data['tempL'][-7:]]
            tempH_list = [round(temp, 1) for temp in daily_data['tempH'][-7:]]
            tempA_list = [round(temp, 1) for temp in daily_data['tempA'][-7:]]
            rhL_list = daily_data['rhL'][-7:]
            rhH_list = daily_data['rhH'][-7:]
            rhA_list = daily_data['rhA'][-7:]
            pressL_list = [round(pressure, 1) for pressure in daily_data['pressL'][-7:]]
            pressH_list = [round(pressure, 1) for pressure in daily_data['pressH'][-7:]]
            pressA_list = [round(pressure, 1) for pressure in daily_data['pressA'][-7:]]
            wavgA_list = [round(speed, 1) for speed in daily_data['wavgA'][-7:]]
            wgustH_list = [round(speed, 1) for speed in daily_data['wgustH'][-7:]]
            wdirA_list = daily_data['wdirA'][-7:]
            precip_list = [round(precip, 1) for precip in daily_data['precip'][-7:]]
            uvH_list = daily_data['uvH'][-7:]
            solarH_list = daily_data['solarH'][-7:]
    
            result = f"Data for station {station_name} for the last 7 days:\n"
            for i in range(7):
                result += f"Date: {datetime_list[i].strftime('%A, %B %d, %Y') if i < len(datetime_list) else '-'}\n"
                result += f"Lowest Temperature: {tempL_list[i] if i < len(tempL_list) else '-'} \N{DEGREE SIGN}C\n"
                result += f"Highest Temperature: {tempH_list[i] if i < len(tempH_list) else '-'} \N{DEGREE SIGN}C\n"
                result += f"Average Temperature: {tempA_list[i] if i < len(tempA_list) else '-'} \N{DEGREE SIGN}C\n"
                result += f"Lowest Relative Humidity: {rhL_list[i] if i < len(rhL_list) else '-'}%\n"
                result += f"Highest Relative Humidity: {rhH_list[i] if i < len(rhH_list) else '-'}%\n"
                result += f"Average Relative Humidity: {rhA_list[i] if i < len(rhA_list) else '-'}%\n"
                result += f"Lowest Pressure: {pressL_list[i] if i < len(pressL_list) else '-'} hPa\n"
                result += f"Highest Pressure: {pressH_list[i] if i < len(pressH_list) else '-'} hPa\n"
                result += f"Average Pressure: {pressA_list[i] if i < len(pressA_list) else '-'} hPa\n"
                result += f"Average Wind Speed: {wavgA_list[i] if i < len(wavgA_list) else '-'} m/s\n"
                result += f"Wind Gust Speed: {wgustH_list[i] if i < len(wgustH_list) else '-'} m/s\n"
                result += f"Wind Direction: {wdirA_list[i] if i < len(wdirA_list) else '-'} \N{DEGREE SIGN}\n"
                result += f"Precipitation: {precip_list[i] if i < len(precip_list) else '-'} mm\n"
                result += f"UV Index: {uvH_list[i] if i < len(uvH_list) else '-'}\n"
                result += f"Solar Radiation: {solarH_list[i] if i < len(solarH_list) else '-'} W/m2\n\n"
    
            tk.Label(self.scrollable_frame, text=result).pack()
    
        except KeyError:
            tk.Label(self.scrollable_frame, text=f"No data available for station {station_name}.)").pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
