import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { AuthService } from 'src/app/api/auth.service';
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
    private authService: AuthService,
  ) { }

  ngOnInit() {
  }

  onSubmit() {
    let email = this.loginForm.value.email
    let password = this.loginForm.value.password
    this.authService.login(email, password)
    .subscribe(token => {
      console.log(token);
    })
  }
    // todo: remove this after dev
    get diagnostic() { return JSON.stringify(this.loginForm.value); }
}
