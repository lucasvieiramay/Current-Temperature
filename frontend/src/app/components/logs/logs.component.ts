import { Component, OnInit } from '@angular/core';
import { LogsService } from '../../services/logs.service';


@Component({
    selector: 'app-logs',
    templateUrl: './logs.component.html',
    styleUrls: ['./logs.component.css']
})
export class LogsComponent implements OnInit {
    logs = [];

    constructor(private logsService:LogsService) { }

    ngOnInit() {
        this.logsService.getLogs().subscribe((logs) => {
            this.logs = logs;
        });
    }
}
