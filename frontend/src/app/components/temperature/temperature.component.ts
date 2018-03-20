import { Component, OnInit } from '@angular/core';
import { WeatherService } from '../../services/weather.service';


@Component({
    selector: 'app-temperature',
    templateUrl: './temperature.component.html',
    styleUrls: ['./temperature.component.scss']
})
export class TemperatureComponent implements OnInit {

    actualTemperature:number;
    maxTemperature:number;
    minTemperature:number;
    city:string;
    rainnyDay = false;
    isDay = false;
    initialized = false;

    constructor(private weatherService:WeatherService) {
    }

    ngOnInit() {
    }

    isEmpty(obj) {
      return Object.keys(obj).length === 0;
    }

    searchTemperature(address){
        if (address) {
            this.weatherService.getCurrentTemperature(address).subscribe((temperature) => {

                this.actualTemperature = Math.round(temperature['temp']);
                this.maxTemperature = Math.round(temperature['temp_max']);
                this.minTemperature = Math.round(temperature['temp_min']);
                this.city = temperature['city'];
                if (this.isEmpty(temperature['rain'])) {
                    this.rainnyDay = false;
                } else {
                    this.rainnyDay = true;
                }
            });
            let hr = (new Date()).getHours();
            if ((hr >= 6) && (hr <= 19)){
                this.isDay = true;
            }
            this.initialized = true;
            return false;
        }
    }
}
