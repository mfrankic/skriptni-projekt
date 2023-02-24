import requests
import tkinter as tk
from bs4 import BeautifulSoup

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
    url = f"https://api.neverin.hr/v2/stations/?station={station_name}"
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
        self.selected_station = tk.StringVar(value=self.station_list[0][0])
        
        self.station_dropdown = tk.OptionMenu(self, self.selected_station, *[station[0] for station in self.station_list])
        self.station_dropdown.pack(pady=10)
        
        self.show_data_button = tk.Button(self, text="Show Data", command=self.show_data)
        self.show_data_button.pack()
        
        self.result_label = tk.Label(self, text="")
        self.result_label.pack(pady=10)
    
    def show_data(self):
        station_name = self.selected_station.get()
        station_data = get_station_data(station_name)
    
        try:
            daily_data = station_data['data']['archive']['daily']
    
            datetime_list = daily_data['datetime'][-7:]
            tempL_list = daily_data['tempL'][-7:]
            tempH_list = daily_data['tempH'][-7:]
            tempA_list = daily_data['tempA'][-7:]
            rhL_list = daily_data['rhL'][-7:]
            rhH_list = daily_data['rhH'][-7:]
            rhA_list = daily_data['rhA'][-7:]
            pressL_list = daily_data['pressL'][-7:]
            pressH_list = daily_data['pressH'][-7:]
            pressA_list = daily_data['pressA'][-7:]
            wavgA_list = daily_data['wavgA'][-7:]
            wgustH_list = daily_data['wgustH'][-7:]
            wdirA_list = daily_data['wdirA'][-7:]
            precip_list = daily_data['precip'][-7:]
            uvH_list = daily_data['uvH'][-7:]
            solarH_list = daily_data['solarH'][-7:]
    
            result = f"Data for station {station_name} for the last 7 days:\n"
            for i in range(7):
                result += f"Date: {datetime_list[i] if i < len(datetime_list) else None}, "
                result += f"Lowest Temp: {tempL_list[i] if i < len(tempL_list) else None}, "
                result += f"Highest Temp: {tempH_list[i] if i < len(tempH_list) else None}, "
                result += f"Average Temp: {tempA_list[i] if i < len(tempA_list) else None}, "
                result += f"Lowest RH: {rhL_list[i] if i < len(rhL_list) else None}, "
                result += f"Highest RH: {rhH_list[i] if i < len(rhH_list) else None}, "
                result += f"Average RH: {rhA_list[i] if i < len(rhA_list) else None}, "
                result += f"Lowest Pressure: {pressL_list[i] if i < len(pressL_list) else None}, "
                result += f"Highest Pressure: {pressH_list[i] if i < len(pressH_list) else None}, "
                result += f"Average Pressure: {pressA_list[i] if i < len(pressA_list) else None}, "
                result += f"Average Wind Speed: {wavgA_list[i] if i < len(wavgA_list) else None}, "
                result += f"Wind Gust Speed: {wgustH_list[i] if i < len(wgustH_list) else None}, "
                result += f"Wind Direction: {wdirA_list[i] if i < len(wdirA_list) else None}, "
                result += f"Precipitation: {precip_list[i] if i < len(precip_list) else None}, "
                result += f"UV Index: {uvH_list[i] if i < len(uvH_list) else None}, "
                result += f"Solar Radiation: {solarH_list[i] if i < len(solarH_list) else None}\n"
    
            self.result_label.configure(text=result)
    
        except KeyError:
            self.result_label.configure(text=f"No data available for station {station_name}.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
