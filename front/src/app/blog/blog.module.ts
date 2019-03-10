import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BoardListComponent } from './components/board-list/board-list.component';
import { PostListComponent } from './components/post-list/post-list.component';
import { PostDetailComponent } from './components/post-detail/post-detail.component';
import { PostFormComponent } from './components/post-form/post-form.component';
import { CommentListComponent } from './components/comment-list/comment-list.component';
import { MainLayoutComponent } from './components/main-layout/main-layout.component';
import { SharedModule } from '../shared/shared.module';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { QuillModule } from 'ngx-quill';
import { BlogRoutingModule } from './blog-routing.module';
import { CommentDeleteComponent } from './components/comment-delete/comment-delete.component';
import { CommentEditComponent } from './components/comment-edit/comment-edit.component';
import { PostNavComponent } from './components/post-nav/post-nav.component';
import { LikeToggleComponent } from './shared/components/like-toggle/like-toggle.component';
import { CommentCreateComponent } from './components/comment-create/comment-create.component';
import { NgxPaginationModule } from 'ngx-pagination';



@NgModule({
  declarations: [
    MainLayoutComponent,
    BoardListComponent,
    PostListComponent,
    PostDetailComponent,
    PostFormComponent,
    CommentListComponent,
    CommentDeleteComponent,
    CommentEditComponent,
    PostNavComponent,
    LikeToggleComponent,
    CommentCreateComponent,
  ],
  imports: [
    CommonModule,
    BlogRoutingModule,
    MatIconModule,
    FormsModule,
    QuillModule,
    ReactiveFormsModule,
    SharedModule,
    NgxPaginationModule,
  ],
  exports: [
    MainLayoutComponent,
  ]
})
export class BlogModule { }
