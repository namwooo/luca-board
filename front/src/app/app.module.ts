import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientInMemoryWebApiModule } from 'angular-in-memory-web-api';
import { HttpClientModule } from '@angular/common/http';
import { MatIconModule } from "@angular/material/icon";
import { QuillModule } from 'ngx-quill';

import { InMemoryDataService } from './services/in-memory-data.service';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BoardListComponent } from './components/board-list/board-list.component';
import { PostListComponent } from './components/post-list/post-list.component';
import { PostDetailComponent } from './components/post-detail/post-detail.component';
import { HeaderComponent } from './components/header/header.component';
import { PostFormComponent } from './components/post-form/post-form.component';
import { FormsModule } from '@angular/forms';
import { QuillEditorComponent } from './shared/components/quill-editor/quill-editor.component';


@NgModule({
  declarations: [
    AppComponent,
    BoardListComponent,
    PostListComponent,
    PostDetailComponent,
    HeaderComponent,
    PostFormComponent,
    QuillEditorComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    HttpClientInMemoryWebApiModule.forRoot(
      InMemoryDataService, { dataEncapsulation: false}
    ),
    MatIconModule,
    FormsModule,
    QuillModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
