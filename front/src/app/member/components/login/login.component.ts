import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { AuthService } from 'src/app/api/auth.service';
import { Router } from '@angular/router';

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
    private router: Router,
  ) { }

  ngOnInit() {
  }

  onSubmit() {
    let email = this.loginForm.value.email
    let password = this.loginForm.value.password
    this.authService.login(email, password)
    .subscribe(token => {
      token ? this.router.navigateByUrl(''): alert('로그인에 실패했습니다. 다시 시도해주세요.');
    })
  }
    // todo: remove this after dev
    get diagnostic() { return JSON.stringify(this.loginForm.value); }
}
