import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './components/login/login.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MemberRoutingModule } from './member-routing.module';
import { ContentOnlyLayoutComponent } from './components/content-only-layout/content-only-layout.component';
import { CookieService } from 'ngx-cookie-service';
import { SignupComponent } from './components/signup/signup.component';

@NgModule({
  declarations: [
    ContentOnlyLayoutComponent,
    LoginComponent,
    SignupComponent,
  ],
  imports: [
    CommonModule,
    FormsModule,
    MemberRoutingModule,
    ReactiveFormsModule,
  ],
  exports: [
    ContentOnlyLayoutComponent, 
  ],
  providers: [CookieService],
})
export class MemberModule { }
