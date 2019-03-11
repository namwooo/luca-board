import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { AuthService } from 'src/app/api/auth.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {
  signupForm = new FormGroup({
    email: new FormControl(''),
    password: new FormControl(''),
    firstName: new FormControl(''),
    lastName: new FormControl(''), 
  })

  constructor(
    private authService: AuthService,
  ) { }

  ngOnInit() {
  }
  onSubmit() {
    let form = this.signupForm.value
    this.authService.signup(form)
    .subscribe(token => {
      console.log(token);
    })
  }

}
