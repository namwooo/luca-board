import { Component, OnInit, Input} from '@angular/core';
import { Validators, FormBuilder } from '@angular/forms';
import { CommentService } from 'src/app/api/comment.service';
import { Comment } from 'src/app/blog/models/comment';

@Component({
  selector: 'app-comment-form',
  templateUrl: './comment-form.component.html',
  styleUrls: ['./comment-form.component.css']
})
export class CommentFormComponent implements OnInit {
  @Input() postId: number;
  @Input() comments: Comment[];
  @Input() targetComment: Comment;
  @Input() isEdit: boolean;

  commentForm = this.formBuilder.group({
    body: ['', Validators.required], 
    })
  
  constructor(
    private commentService: CommentService,
    private formBuilder: FormBuilder,
  ) { }

  ngOnInit() {
    this.setCommentEditForm();
  }

  setCommentEditForm() {
    if(this.isEdit) {
      this.commentForm = this.formBuilder.group({
        body: [this.targetComment.body, Validators.required], 
        })
    }
  }

  onSubmit(): void {
    this.commentService.createComment(this.commentForm.value, this.postId, this.targetComment)
    .subscribe(comment => {
      console.log(comment)
      /* 댓글 생성 시, 댓글 삽입 위치를 결정하는 로직 
         1. 루트 댓글은 댓글 창 맨 아래 삽입
         2. 답글은 타겟 댓글 트리 맨 아래 삽입
         3. 답글에 대한 답글도 타겟 댓글 트리 맨 아래 삽입 */
      if(this.targetComment) {
        // 답글을 달려는 타겟 댓글 인덱스
        let targetCommentIndex = this.comments.map(comment => comment.id).indexOf(this.targetComment.id)
        console.log(targetCommentIndex)

        // 타겟 댓글 이후 첫 루트 댓글에 대한 인덱스
        // 타겟 댓글 인덱스 + 1 부터 검색하여 level 0인 첫번쨰 댓글 인덱스 추출
        let firstRootCommentIndex = this.comments.map(comment => comment.level).indexOf(0, targetCommentIndex+1)
        console.log(firstRootCommentIndex)

        if (firstRootCommentIndex === -1) {
          // 타겟 댓글이 마지막 루트 댓글인 경우, 맨 아래 삽입
          this.comments.push(comment);
        } else {
          // 타겟 댓글 인덱스에 댓글 차이 
          this.comments.splice(targetCommentIndex + (firstRootCommentIndex - targetCommentIndex), 0, comment);
        }
      } else {
        // 타겟 댓글이 없으면 맨 아래에 삽입
        this.comments.push(comment);
      }
      this.commentForm.reset();
    })
  }
}
