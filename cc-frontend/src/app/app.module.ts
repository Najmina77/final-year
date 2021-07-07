import { BrowserModule } from '@angular/platform-browser';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FarmerModule } from './feature modules/farmer.module';
import { WeatherService } from './Services/weather.service';
import { HttpClientModule } from '@angular/common/http';






@NgModule({
  declarations: [
    AppComponent,


  ],
  imports: [
    BrowserAnimationsModule,
    HttpClientModule,
    BrowserModule,
    FarmerModule,
    AppRoutingModule
  ],


  providers: [
    WeatherService,
  ],

  exports: [
    HttpClientModule,
  ],
  
  bootstrap: [AppComponent]
})
export class AppModule { }
 