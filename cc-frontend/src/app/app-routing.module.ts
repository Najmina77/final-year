import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { FarmerComponent } from './Components/farmer/farmer.component';

const routes: Routes = [
  {path:'home', component:FarmerComponent},
  {path:'', redirectTo:'home', pathMatch:'full'},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
