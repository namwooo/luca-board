import { Component, OnInit } from '@angular/core';
import { Post } from 'src/app/blog/models/post';
import { PostService } from 'src/app/api/post.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-post-detail',
  templateUrl: './post-detail.component.html',
  styleUrls: ['./post-detail.component.css']
})
export class PostDetailComponent implements OnInit {
  post: Post;
  // update require id

  constructor(
    private postService: PostService,
    private route: ActivatedRoute,
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

  editPost(id: number): void {
    
  }

  deletePost(id: number): void {
    
  }
}
