import { AfterViewInit, Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-prediction',
  templateUrl: './prediction.component.html',
  styleUrls: ['./prediction.component.css']
})
export class PredictionComponent implements OnInit, AfterViewInit {
 pred: FormGroup;
 predd: boolean = true;

  constructor(private fb: FormBuilder) { }
 

  ngOnInit(): void {
    this.pred = this.fb.group({
      location: new FormControl(''),
      duration: new FormControl('')

    })
  }
  ngAfterViewInit(): void {
  
  }

}
