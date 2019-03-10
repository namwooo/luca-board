import { Component, OnInit, Input } from '@angular/core';
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
  parentCommentId: number;
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

  onCreated(createdComment: Comment) {
    if(createdComment) {
        /* 댓글 생성 시, 댓글 삽입 위치를 결정하는 로직 
        1. 루트 댓글은 댓글 창 맨 아래 삽입
        2. 답글은 타겟 댓글 트리 맨 아래 삽입
        3. 답글에 대한 답글도 타겟 댓글 트리 맨 아래 삽입 */
        if(this.parentCommentId) {
          // 답글을 달려는 타겟 댓글 인덱스
          let parentCommentIndex = this.comments.map(comment => comment.id).indexOf(this.parentCommentId)
          console.log(parentCommentIndex)
  
          // 타겟 댓글 이후 첫 루트 댓글에 대한 인덱스
          // 타겟 댓글 인덱스 + 1 부터 검색하여 level 0인 첫번쨰 댓글 인덱스 추출
          let firstRootCommentIndex = this.comments.map(comment => comment.level).indexOf(0, parentCommentIndex+1)
          console.log(firstRootCommentIndex)
  
          if (firstRootCommentIndex === -1) {
            // 타겟 댓글이 마지막 루트 댓글인 경우, 맨 아래 삽입
            this.comments.push(createdComment);
          } else {
            // 타겟 댓글 인덱스에 댓글 차이 
            this.comments.splice(parentCommentIndex + (firstRootCommentIndex - parentCommentIndex), 0, createdComment);
          }
        } else {
          // 타겟 댓글이 없으면 맨 아래에 삽입
          this.comments.push(createdComment);
        }
    }
    this.isCommentFormInserted = false;
    
  }

  onDeleted(deletedComment: Comment) {
    if (deletedComment) {
      let index = this.comments.findIndex(c => c.id === deletedComment.id);
      this.comments.splice(index, 1);
    } else {
      void 0;
    }
  }

  onEdited(body: string) {
    if (body) {
      let comment = this.comments.find(c => c.id === this.targetCommentId);
      comment.body = body
      this.isCommentEditFormInserted = false;
    } else {
      void 0;
    }
  }
  
  insertCommentForm(comment: Comment) {
    if (this.parentCommentId != comment.id) {
      this.parentCommentId = comment.id;
    } else if (this.isCommentFormInserted) {
      this.isCommentFormInserted = false;
    } else {
      this.parentCommentId = comment.id;
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
