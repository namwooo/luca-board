import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PostListComponent } from './components/post-list/post-list.component';
import { PostDetailComponent } from './components/post-detail/post-detail.component';
import { PostFormComponent } from './components/post-form/post-form.component';
import { LoginComponent } from './components/login/login.component';
import { MainLayoutComponent } from './components/main-layout/main-layout.component';
import { ContentOnlyLayoutComponent } from './components/content-only-layout/content-only-layout.component';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'boards/1',
    pathMatch: 'full',
  },
  {
    path: '',
    component: MainLayoutComponent,
    children: [
      { path: 'boards/:id', component: PostListComponent },
      { path: 'posts/:id', component: PostDetailComponent },
      { path: 'posts', component: PostFormComponent },
    ]
  },
  {
    path: '',
    component: ContentOnlyLayoutComponent,
    children: [
      { path: 'login', component: LoginComponent},
    ]
  }

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
