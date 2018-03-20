import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

import 'rxjs/add/operator/map';


@Injectable()
export class WeatherService {

    constructor(public http:Http) {
    }

    getCurrentTemperature(address){
        let data = {
            'address': address,
            'unit_of_measurement': 'celsius'
        };
        return this.http.post("http://localhost:8000/api/", data)
              .map(response => response.json())
    }
}
