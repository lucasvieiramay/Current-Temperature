// Angular imports
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';
import { RouterModule, Routes } from '@angular/router';

// Components imports
import { AppComponent } from './app.component';
import { TemperatureComponent } from './components/temperature/temperature.component';
import { LogsComponent } from './components/logs/logs.component';

// Services imports
import { WeatherService } from './services/weather.service';
import { LogsService } from './services/logs.service';


const appRoutes: Routes = [
  { path: '',      component: TemperatureComponent },
  { path: 'logs',  component: LogsComponent },
];


@NgModule({
  declarations: [
    AppComponent,
    TemperatureComponent,
    LogsComponent
  ],
  imports: [
    RouterModule.forRoot(appRoutes),
    BrowserModule,
    HttpModule
  ],
  providers: [WeatherService, LogsService], // Here we declarate the services
  bootstrap: [AppComponent]
})
export class AppModule { }
