import { Component, OnInit } from '@angular/core';
import {Store, select} from '@ngrx/store';
import { SET_LOCATION } from '../../../location-reducer';
import { NgForm } from '@angular/forms';
import { Observable} from 'rxjs';


@Component({
  selector: 'app-farmer-home',
  templateUrl: './farmer-home.component.html',
  styleUrls: ['./farmer-home.component.css']
})
export class FarmerHomeComponent implements OnInit {
  loc$: Observable<string>;
  loc: string = '';  
  constructor(private store: Store<any>) {
    this.loc$ = store.pipe(select('loc'));
    this.loc$.subscribe(loc => {
      this.loc = loc;
    })
  }

  ngOnInit(): void {
  }

  search(searchForm: NgForm) {
    if (searchForm.invalid) {
      return;
    }
    this.store.dispatch({ type: SET_LOCATION, payload: this.loc });
  }

}
