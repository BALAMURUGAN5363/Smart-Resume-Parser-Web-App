import { Component, OnInit, PLATFORM_ID, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  historyData: any[] = [];
  lastExtractedData: any = null;
  isLoggedIn = false;
  historyVisible = false;
  trialDownloadCount = 0;
  maxTrialDownloads = 5;

  selectedFile: File | null = null;
  extractedVisible = false;

  constructor(
    private http: HttpClient, 
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  ngOnInit() {
    this.loadHistory();
    if (isPlatformBrowser(this.platformId)) {
      const savedCount = localStorage.getItem('trialDownloadCount');
      this.trialDownloadCount = savedCount ? parseInt(savedCount, 10) : 0;
    }
  }

  loadHistory() {
    if (isPlatformBrowser(this.platformId)) {
      const savedHistory = localStorage.getItem('conversionHistory');
      if (savedHistory) {
        this.historyData = JSON.parse(savedHistory);
      }
    }
  }

  processFile(file: File) {
    const extracted = {
      fileName: file.name,
      content: {
        message: `Resume data extracted from ${file.name}`,
        timestamp: new Date().toISOString()
      }
    };

    this.lastExtractedData = extracted;
    this.historyData.push(extracted);
    
    if (isPlatformBrowser(this.platformId)) {
      localStorage.setItem('conversionHistory', JSON.stringify(this.historyData));
    }
  }

  navigateToHistory() {
    if (!this.isLoggedIn && this.trialDownloadCount >= this.maxTrialDownloads) {
      alert('You have reached the maximum trial limit. Please login or sign up to continue.');
      this.router.navigate(['/login']);
      return;
    }
    this.router.navigate(['/history']);
  }

  handleDownloadRequest(index?: number) {
    if (!this.isLoggedIn) {
      if (this.trialDownloadCount >= this.maxTrialDownloads) {
        alert('You have reached the maximum trial limit. Please login or sign up to continue.');
        this.router.navigate(['/login']);
        return;
      }
      this.trialDownloadCount++;
      if (isPlatformBrowser(this.platformId)) {
        localStorage.setItem('trialDownloadCount', this.trialDownloadCount.toString());
      }
    }
    this.downloadJson(index);
  }

  onExtractClicked() {
    if (!this.selectedFile) {
      alert('Please select a file.');
      return;
    }

    if (!this.isLoggedIn && this.trialDownloadCount >= this.maxTrialDownloads) {
      alert('You have reached the maximum trial limit. Please login or sign up to continue.');
      this.router.navigate(['/login']);
      return;
    }

    const fileSizeGB = this.selectedFile.size / (1024 * 1024 * 1024);
    if (fileSizeGB > 5 && !this.isLoggedIn) {
      this.router.navigate(['/login']);
      return;
    }

    this.processFile(this.selectedFile);
    this.extractedVisible = true;
  }

  downloadJson(index?: number) {
    if (isPlatformBrowser(this.platformId)) {
      const dataToDownload = index !== undefined ? this.historyData[index] : this.lastExtractedData;
      if (dataToDownload) {
        const blob = new Blob([JSON.stringify(dataToDownload.content, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = dataToDownload.fileName.replace(/\.[^/.]+$/, '') + '.json';
        a.click();
        URL.revokeObjectURL(url);
      }
    }
  }

  navigateToLogin() {
    this.router.navigate(['/login']);
  }

  navigateToSignup() {
    this.router.navigate(['/signup']);
  }

  logout() {
    this.isLoggedIn = false;
    this.trialDownloadCount = 0;
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem('trialDownloadCount');
    }
    this.router.navigate(['/']);
  }

  storeSelectedFile(event: Event) {
    const input = event.target as HTMLInputElement;
    this.selectedFile = input.files?.[0] || null;
  }
}