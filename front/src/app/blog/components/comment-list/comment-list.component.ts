import { Component, OnInit, Input, ViewChild } from '@angular/core';
import { CommentService } from 'src/app/api/comment.service';
import { Comment } from 'src/app/blog/models/comment';

@Component({
  selector: 'app-comment-list',
  templateUrl: './comment-list.component.html',
  styleUrls: ['./comment-list.component.css']
})
export class CommentListComponent implements OnInit {
  @Input() postId: number;
  comments: Comment[];
  targetCommentId: number;
  isCommentFormInserted = false;
  isCommentEditFormInserted = false;

  constructor(
    private commentService: CommentService,
  ) { }

  ngOnInit() {
    this.getCommentsInPost(this.postId);
  }

  getCommentsInPost(postId: number) {
    this.commentService.getCommentsInPost(postId)
    .subscribe(comments => {this.comments = comments
      console.log(this.comments)})
  }

  onDeleted(deletedComment: Comment) {
    if (deletedComment) {
      let index = this.comments.findIndex(c => c.id === deletedComment.id);
      this.comments.splice(index, 1);
    } else {
      void 0;
    }
  }
  
  insertCommentForm(comment: Comment) {
    if (this.targetCommentId != comment.id) {
      this.targetCommentId = comment.id;
    } else if (this.isCommentFormInserted) {
      this.isCommentFormInserted = false;
    } else {
      this.targetCommentId = comment.id;
      this.isCommentFormInserted= true;
    }
  }

  insertCommentEditForm(comment) {
    if (this.targetCommentId != comment.id) {
      this.targetCommentId = comment.id;
      this.isCommentEditFormInserted= true;
    } else if (this.isCommentEditFormInserted) {
      this.isCommentEditFormInserted = false;
    } else {
      this.targetCommentId = comment.id;
      this.isCommentEditFormInserted= true;
    }

  }
}
