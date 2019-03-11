import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  isLogin: boolean;
  
  constructor(
    private router: Router,
  ) { }

  ngOnInit() {
    if (localStorage.getItem('access_token')) {
      this.isLogin = true;
    } else {
      this.isLogin = false;
    }
  }
  
  onClickLogin() {
    this.router.navigate(['/user/login'])
  }

  onClickLogout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('expires_at')
    this.isLogin = false;
  }

}
