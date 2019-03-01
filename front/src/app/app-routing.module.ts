import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MainLayoutComponent } from './blog/components/main-layout/main-layout.component';
import { ContentOnlyLayoutComponent } from './member/components/content-only-layout/content-only-layout.component';
import { PostListComponent } from './blog/components/post-list/post-list.component';
import { PostDetailComponent } from './blog/components/post-detail/post-detail.component';

const routes: Routes = [
  { path: '', loadChildren: './blog/blog.module#BlogModule' },
  { path: 'member', loadChildren: './member/member.module#MemberModule' }, 
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
