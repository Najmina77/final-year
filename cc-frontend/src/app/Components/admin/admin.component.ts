import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})
export class AdminComponent implements OnInit {
  sideBarOpen = true;

  constructor() { }

  ngOnInit(): void {
    
  }
  toggleSideBar(){
    this.sideBarOpen = !this.sideBarOpen;
  }
  signOut(){
    window.location.href="http://127.0.0.1:8000/logout/";
  }

}
