import { Component, OnInit, OnChanges, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { Post } from 'src/app/models/post';
import { PostService } from 'src/app/services/post.service';
import { BoardService } from 'src/app/services/board.service';
import { Board } from 'src/app/models/board';

@Component({
  selector: 'app-post-list',
  templateUrl: './post-list.component.html',
  styleUrls: ['./post-list.component.css']
})
export class PostListComponent implements OnInit {
  posts: Post[];
  board: Board;
  
  constructor(
    private postService: PostService,
    private boardService: BoardService,
    private route: ActivatedRoute,
    ) { }
  
  ngOnInit() {
    this.route.params.subscribe(
      params => {
        let id = +params['id']
        this.getBoard(id);
        this.getPostsInBoard(id);
      }
    )
  }

  getPostsInBoard(id: number): void {
    const board_id = +this.route.snapshot.paramMap.get('id')
    this.postService.getPostsInBoard(board_id)
    .subscribe(posts => this.posts = posts)
  }
  getBoard(id: number): void {
    const board_id = +this.route.snapshot.paramMap.get('id')
    this.boardService.getBoard(board_id)
    .subscribe(board => this.board = board)
  }
}
