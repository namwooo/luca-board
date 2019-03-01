import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { LoginService } from 'src/app/api/login.service';
import * as camelCaseKeys from 'camelcase-keys';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm = new FormGroup({
    email: new FormControl(''),
    password: new FormControl(''), 
  })

  constructor(
    private loginService: LoginService,
    private cookieService: CookieService,
  ) { }

  ngOnInit() {
  }

  onSubmit() {
    this.loginService.login(this.loginForm.value)
    .subscribe(user => {
      console.log(user);
      // this.cookieService.set('remeber_token', user.id);
    })
  }
    // todo: remove this after dev
    get diagnostic() { return JSON.stringify(this.loginForm.value); }
}
