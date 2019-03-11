import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { ContentOnlyLayoutComponent } from './components/content-only-layout/content-only-layout.component';

const routes: Routes = [
    { 
      path: '', component: ContentOnlyLayoutComponent,  
      children: [    
          { path: 'login', component: LoginComponent },
      ]
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MemberRoutingModule { }
