import { Component, OnInit } from '@angular/core';
import { Board } from 'src/app/blog/models/board';
import { BoardService } from 'src/app/api/board.service';

@Component({
  selector: 'app-board-list',
  templateUrl: './board-list.component.html',
  styleUrls: ['./board-list.component.css']
})
export class BoardListComponent implements OnInit {
  boards: Board[];
  selectedBoard: Board;

  constructor(private boardService: BoardService) {}

  ngOnInit() {
    this.getBoards();
  }

  getBoards(): void {
    this.boardService.getBoards()
    .subscribe(boards => this.boards = boards);
  }
}
