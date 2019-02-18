import { Component, OnInit, OnChanges } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { Post } from 'src/app/models/post';
import { PostService } from 'src/app/services/post.service';

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

  getPostsInBoard(id: number): void {
    const board_id = +this.route.snapshot.paramMap.get('id')
    this.postService.getPostsInBoard(board_id)
    .subscribe(posts => this.posts = posts)
  }

}
