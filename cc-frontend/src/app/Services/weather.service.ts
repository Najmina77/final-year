import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import * as moment from 'moment';


@Injectable({
  providedIn: 'root'
})
export class WeatherService {
  apiKey: string = '2ea08a6054174baf92f7490f638e6d43';
  apiUrl:string = 'http://api.openweathermap.org/data/2.5';

  constructor(private http: HttpClient) { }  
  
  getCurrentWeather(loc: string) {
    return this.http.get(`${this.apiUrl}/weather?q=${loc}&appid=${this.apiKey}`)
  }  
  getForecast(loc: string) {
    return this.http.get(`${this.apiUrl}/forecast?q=${loc}&appid=${this.apiKey}`)
  }  
  getUv(lat: number, lon: number) {
    let startDate = Math.round(+moment(new Date()).subtract(1, 'week').toDate() / 1000);
    let endDate = Math.round(+moment(new Date()).add(1, 'week').toDate() / 1000);
    return this.http.get(`${this.apiUrl}/uvi/history?lat=${lat}&lon=${lon}&start=${startDate}&end=${endDate}&appid=${this.apiKey}`)
  }
}



