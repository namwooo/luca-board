import { Component, OnInit } from '@angular/core';
import { Board } from 'src/app/models/board';
import { BoardService } from 'src/app/services/board.service';
import { PostForm } from 'src/app/models/post-form';

@Component({
  selector: 'app-post-form',
  templateUrl: './post-form.component.html',
  styleUrls: ['./post-form.component.css']
})
export class PostFormComponent implements OnInit {
  boards: Board[];

  postForm = new PostForm(true);

  constructor(private boardService: BoardService) { }

  ngOnInit() {
    this.getBoards();
  }

  onSubmit() {
    console.log('submit')
    console.log(this.postForm);
  }

  getBoards(): void {
    this.boardService.getBoards()
    .subscribe(boards => this.boards = boards);
  }
}