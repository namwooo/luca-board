import { Component, OnInit } from '@angular/core';
import * as ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import { ChangeEvent } from '@ckeditor/ckeditor5-angular/ckeditor.component';
import { Board } from 'src/app/models/board';
import { BoardService } from 'src/app/services/board.service';
import { Post } from 'src/app/models/post';
import { PostForm } from 'src/app/models/post-form';

@Component({
  selector: 'app-post-form',
  templateUrl: './post-form.component.html',
  styleUrls: ['./post-form.component.css']
})
export class PostFormComponent implements OnInit {
  public Editor = ClassicEditor;
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

  public onChange( { editor }: ChangeEvent ) {
    const data = editor.getData();

    console.log( data );
  }

  getBoards(): void {
    this.boardService.getBoards()
    .subscribe(boards => this.boards = boards);
  }
}