import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

import 'rxjs/add/operator/map';


@Injectable()
export class LogsService {

    constructor(public http:Http) { }

    getLogs(){
      return this.http.get("http://localhost:8000/api/list-logs").map(
            response => response.json());
    }
}
