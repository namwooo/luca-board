import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PostDetailComponent } from './components/post-detail/post-detail.component';
import { PostListComponent } from './components/post-list/post-list.component';
import { MainLayoutComponent } from './components/main-layout/main-layout.component';
import { PostFormComponent } from './components/post-form/post-form.component';

const routes: Routes = [
    { 
        path: '', component: MainLayoutComponent,  
        children: [    
            { path: 'boards/:id', component: PostListComponent },
            { path: 'boards', component: PostListComponent },
            { path: 'posts/:id', component: PostDetailComponent },
            { path: 'posts', component: PostFormComponent },

        ]
    },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class BlogRoutingModule { }
