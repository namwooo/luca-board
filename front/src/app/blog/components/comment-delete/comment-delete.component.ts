import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { CommentService } from 'src/app/api/comment.service';
import { Comment } from 'src/app/blog/models/comment';

@Component({
  selector: 'app-comment-delete',
  template: `<a (click)="onClickDelete(targetComment)">삭제</a>`,
  styleUrls: ['./comment-delete.component.css']
})
export class CommentDeleteComponent implements OnInit {
  @Input() targetComment: Comment;
  @Output() deleted = new EventEmitter<Comment>();

  constructor(
    private commentService: CommentService,
  ) { }

  ngOnInit() {
  }

  onClickDelete(deletedComment: Comment) {
    let commentId = this.targetComment.id
    this.commentService.deleteComment(commentId)
    .subscribe(resp => {
      this.deleted.emit(deletedComment);
    })
  }

}
