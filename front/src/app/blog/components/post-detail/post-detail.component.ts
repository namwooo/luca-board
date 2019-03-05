import { Component, OnInit } from '@angular/core';
import { Post } from 'src/app/blog/models/post';
import { PostService } from 'src/app/api/post.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-post-detail',
  templateUrl: './post-detail.component.html',
  styleUrls: ['./post-detail.component.css']
})
export class PostDetailComponent implements OnInit {
  post: Post;

  constructor(
    private postService: PostService,
    private route: ActivatedRoute,
    private router: Router,
    ) { }

  ngOnInit() {
    this.route.params.subscribe(
      params => {
        let id = +params['id']
        this.getPost(id);
      }
    )
  }

  getPost(id: number): void {
    this.postService.getPost(id)
    .subscribe(post => this.post = post)
  }

  onClickEdit(): void {
    let postId = this.post.id
    
    this.router.navigate([`/posts/${postId}/edit`])
  }

  onClickDelete(): void {
    let postId = this.post.id
    let boardId = this.post.board.id

    this.postService.deletePost(postId)
    .subscribe(resp => {
      this.router.navigate([`/boards/${boardId}`,])
    })
  }
}
