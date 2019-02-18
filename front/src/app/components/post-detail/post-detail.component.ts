import { Component, OnInit } from '@angular/core';
import { Post } from 'src/app/models/post';
import { PostService } from 'src/app/services/post.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-post-detail',
  templateUrl: './post-detail.component.html',
  styleUrls: ['./post-detail.component.css']
})
export class PostDetailComponent implements OnInit {
  post: Post[];

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
    const post_id = +this.route.snapshot.paramMap.get('id')
    this.postService.getPost(post_id)
    .subscribe(post => this.post = post)
  }
}
