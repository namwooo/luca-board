import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-logo',
  template: '<a><img src="assets/images/logo.png"></a>',
  styleUrls: ['./logo.component.css']
})
export class LogoComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}
