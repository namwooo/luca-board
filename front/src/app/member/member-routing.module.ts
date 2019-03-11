import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { ContentOnlyLayoutComponent } from './components/content-only-layout/content-only-layout.component';
import { SignupComponent } from './components/signup/signup.component';

const routes: Routes = [
    { 
      path: 'user', component: ContentOnlyLayoutComponent,  
      children: [
          { path: 'signup', component: SignupComponent },    
          { path: 'login', component: LoginComponent },
      ]
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MemberRoutingModule { }
