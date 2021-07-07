import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';


import { FlexLayoutModule } from '@angular/flex-layout';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDividerModule } from '@angular/material/divider';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { MatMenuModule } from '@angular/material/menu';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatStepperModule } from '@angular/material/stepper';
import { MatToolbarModule } from '@angular/material/toolbar';
import {MatTabsModule} from '@angular/material/tabs';
import { StoreModule } from '@ngrx/store';
import { RouterModule } from '@angular/router';
// import { NgxChartsModule } from '@swimlane/ngx-charts';
import {MatDialogModule } from '@angular/material/dialog';
// import {NgxPrintModule} from 'ngx-print';

import { FarmerComponent } from '../Components/farmer/farmer.component';
import { FarmerHomeComponent } from '../Components/farmer/farmer-home/farmer-home.component';
import { CurrentWeatherComponent } from '../Services/current-weather/current-weather.component';
import { ForecastComponent } from '../Services/forecast/forecast.component';
import { UvComponent } from '../Services/uv/uv.component';
import { locationReducer } from '../location-reducer';
import { PredictionComponent } from '../Components/prediction/prediction.component';
import { AdminComponent } from '../Components/admin/admin.component';
import { RecordsComponent } from '../Components/records/records.component';


@NgModule({

    declarations: [
        FarmerComponent,
        FarmerHomeComponent,
        CurrentWeatherComponent,
        ForecastComponent,
        UvComponent,
        PredictionComponent,
        AdminComponent,
        RecordsComponent,


    ], 

    imports: [
        RouterModule.forChild([
            {
                path: 'st-farmer', component: FarmerComponent,
                children: [
                    {path:'home', component: FarmerHomeComponent},
                    {path:'predict', component: PredictionComponent},
                    {path:'', redirectTo:"home", pathMatch:"full"},
                ]
                
            //     children: [
            //         {path: "dashboard", component: DashboardComponent,
            //         // display the application form within the student dashboard
            //         children: [
            //             {path: "apply", component: BursaryApplicationComponent},
            //         ]},
            //         {path: "st-profile", component: ProfileComponent}, 
            //         {path: "st-notifications", component: NotificationsComponent},
            //         {path: 'cheque', component:ChequeComponent},
            //         {path: 'cheque/:id', component:ChequeComponent},
            //         {path: "st-applications", component: AgingApplicationsComponent},
            //         // {path: "st-notifications", component:},
            //         {path: '', redirectTo: "dashboard", pathMatch: "full" }
            //     ] 
            // },
            // {path: 'chq', component:ChequeComponent},
            },
            // {path:'', redirectTo:'st-farmer/home', pathMatch:'full'},

            {
                path: 'ds-admin', component:AdminComponent,
                children: [
                    {path: 'record', component: RecordsComponent},
                    {path:'', redirectTo:'record', pathMatch:"full"},
                ]
            }

        ]),

       CommonModule,
        MatTabsModule,
        MatButtonModule,
        MatCardModule,
        MatIconModule,
        MatToolbarModule,
        MatMenuModule,
        ReactiveFormsModule,
        FormsModule,
        FlexLayoutModule,
        MatStepperModule,
        MatListModule,
        MatDividerModule,
        MatSidenavModule,
        // NgxChartsModule,
        // DataTablesModule,
        MatDialogModule,
        StoreModule.forRoot({
            loc: locationReducer
        }),
        // NgxPrintModule,

    ], 


    
    

})

export class FarmerModule {

}