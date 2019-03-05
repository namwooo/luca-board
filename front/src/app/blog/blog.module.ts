import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BoardListComponent } from './components/board-list/board-list.component';
import { PostListComponent } from './components/post-list/post-list.component';
import { PostDetailComponent } from './components/post-detail/post-detail.component';
import { PostFormComponent } from './components/post-form/post-form.component';
import { CommentListComponent } from './components/comment-list/comment-list.component';
import { CommentFormComponent } from './components/comment-form/comment-form.component';
import { MainLayoutComponent } from './components/main-layout/main-layout.component';
import { SharedModule } from '../shared/shared.module';
import { AppRoutingModule } from '../app-routing.module';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { QuillModule } from 'ngx-quill';
import { BlogRoutingModule } from './blog-routing.module';


@NgModule({
  declarations: [
    MainLayoutComponent,
    BoardListComponent,
    PostListComponent,
    PostDetailComponent,
    PostFormComponent,
    CommentListComponent,
    CommentFormComponent,
  ],
  imports: [
    CommonModule,
    BlogRoutingModule,
    MatIconModule,
    FormsModule,
    QuillModule,
    ReactiveFormsModule,
    SharedModule,
  ],
  exports: [
    MainLayoutComponent,
  ]
})
export class BlogModule { }
