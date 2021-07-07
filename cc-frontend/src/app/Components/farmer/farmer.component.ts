import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-farmer',
  templateUrl: './farmer.component.html',
  styleUrls: ['./farmer.component.css']
})
export class FarmerComponent implements OnInit {
  logoutUrl:string = 'http://127.0.0.1:8000/logout/';
  sideBarOpen = true;


  constructor() { }

  ngOnInit(): void {
  }

  toggleSideBar(){
    this.sideBarOpen = !this.sideBarOpen;
  }

  signOut(){
    window.location.href = this.logoutUrl;
  }

}
