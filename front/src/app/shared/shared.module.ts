import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from './components/header/header.component';
import { LogoComponent } from './components/logo/logo.component';
import { LoginComponent } from './components/login/login.component';

@NgModule({
  declarations: [
    HeaderComponent,
    LogoComponent,
    LoginComponent,
  ],
  imports: [
    CommonModule
  ],
  exports: [
    HeaderComponent,
    LogoComponent,
    LoginComponent,
  ]
})
export class SharedModule { }
