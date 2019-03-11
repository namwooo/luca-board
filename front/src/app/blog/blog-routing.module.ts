import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PostDetailComponent } from './components/post-detail/post-detail.component';
import { PostListComponent } from './components/post-list/post-list.component';
import { MainLayoutComponent } from './components/main-layout/main-layout.component';
import { PostFormComponent } from './components/post-form/post-form.component';
import { BoardListComponent } from './components/board-list/board-list.component';

const routes: Routes = [
    { 
        path: '', component: MainLayoutComponent,
        children: [    
            { path: 'boards/:id', component: PostListComponent},
            { path: 'posts/:id/edit', component: PostFormComponent, data: {isEdit: true} },
            { path: 'posts/:id', component: PostDetailComponent },
            { path: 'posts', component: PostFormComponent, data: {isEdit: false} },

        ]
    },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class BlogRoutingModule { }
