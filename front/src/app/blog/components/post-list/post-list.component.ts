import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { Post, PagedPost } from 'src/app/blog/models/post';
import { PostService } from 'src/app/api/post.service';

@Component({
  selector: 'app-post-list',
  templateUrl: './post-list.component.html',
  styleUrls: ['./post-list.component.css']
})
export class PostListComponent implements OnInit {
  posts: Post[];
  
  constructor(
    private postService: PostService,
    private route: ActivatedRoute,
    ) { }
  
  ngOnInit() {
    this.route.params.subscribe(
      params => {
        let id = +params['id']
        this.getPostsInBoard(id);
      }
    )
  }

  getPostsInBoard(boardId: number): void {
    this.postService.getPostsInBoard(boardId)
    .subscribe(posts => {
      this.posts = posts['items']
    });

  }
}
