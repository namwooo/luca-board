import { Component, OnInit, Input } from '@angular/core';
import { CommentService } from 'src/app/services/comment.service';
import { Comment } from 'src/app/models/comment';
import { Post } from 'src/app/models/post';

@Component({
  selector: 'app-comment-list',
  templateUrl: './comment-list.component.html',
  styleUrls: ['./comment-list.component.css']
})
export class CommentListComponent implements OnInit {
  @Input() post: Post;
  comments: Comment[];
  idComment: number;
  addComment = false;

  constructor(
    private commentService: CommentService,
  ) { }

  ngOnInit() {
    this.getCommentsInPost(this.post.id);
  }

  getCommentsInPost(idPost: number) {
    this.commentService.getCommentsInPost(idPost)
    .subscribe(comments => this.comments = comments)
  }
  
  addCommentForm(event: any) {
    this.idComment = event.target.id;
    if (this.addComment) {
      this.addComment = false;
    } else {
      this.addComment= true;
    }
  }
}
