import { Document, Page, pdfjs } from "react-pdf";

// CSS for react-pdf
import "react-pdf/dist/Page/AnnotationLayer.css";
import "react-pdf/dist/Page/TextLayer.css";

// Worker configuration
pdfjs.GlobalWorkerOptions.workerSrc = "/pdfjs/pdf.worker.min.mjs";

export default function PdfViewer({ file, page }) {
  if (!file) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center p-8 bg-[#0a0f18] rounded-2xl border-2 border-dashed border-slate-800">
        <div className="w-16 h-16 bg-slate-800/50 rounded-full flex items-center justify-center mb-4">
          <i className="fas fa-file-pdf text-slate-600 text-2xl" />
        </div>
        <h4 className="text-slate-300 font-semibold">No Document Selected</h4>
        <p className="text-slate-500 text-sm mt-2 max-w-[200px]">
          Click on a citation in the chat to preview the source material here.
        </p>
      </div>
    );
  }

  const pdfUrl = `https://pdf-ai-app-bm00.onrender.com/uploads/${encodeURIComponent(file)}`;

  return (
    <div className="flex flex-col h-full bg-[#030712] rounded-2xl overflow-hidden border border-slate-800 shadow-2xl animate-in fade-in zoom-in-95 duration-300">
      {/* PDF Header bar */}
      <div className="bg-[#111827] px-5 py-3 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-3 overflow-hidden">
          <i className="fas fa-file-pdf text-red-500" />
          <span className="text-xs font-bold text-slate-300 truncate tracking-tight">
            {file}
          </span>
        </div>
        <div className="flex items-center gap-2">
           <span className="text-[10px] font-bold bg-blue-500/10 text-blue-400 px-2 py-1 rounded">
             PAGE {page || 1}
           </span>
        </div>
      </div>

      {/* PDF Content Area */}
      <div className="flex-1 overflow-auto p-4 flex justify-center bg-slate-900/40 custom-scrollbar">
        <div className="shadow-[0_0_50px_rgba(0,0,0,0.5)] rounded-sm overflow-hidden">
          <Document
            file={pdfUrl}
            loading={
              <div className="flex flex-col items-center py-20">
                <i className="fas fa-circle-notch fa-spin text-blue-500 text-2xl mb-4" />
                <p className="text-slate-400 text-xs font-medium uppercase tracking-widest">
                  Rendering Document...
                </p>
              </div>
            }
            error={
              <div className="p-10 text-center">
                <i className="fas fa-exclamation-triangle text-red-500 mb-2" />
                <p className="text-red-400 text-sm">Failed to load PDF file.</p>
                <button 
                  onClick={() => window.location.reload()}
                  className="mt-4 text-[10px] text-blue-400 underline"
                >
                  Retry Connection
                </button>
              </div>
            }
          >
            <Page 
              pageNumber={page || 1} 
              scale={1.2}
              renderTextLayer={true}
              renderAnnotationLayer={true}
              className="rounded-sm"
            />
          </Document>
        </div>
      </div>
      
      {/* Optional Footer controls */}
      <div className="bg-[#111827] px-4 py-2 border-t border-slate-800 flex justify-center gap-4">
        <button className="text-slate-500 hover:text-white transition cursor-not-allowed">
          <i className="fas fa-search-minus text-xs" />
        </button>
        <span className="text-[10px] text-slate-600 font-bold self-center">120%</span>
        <button className="text-slate-500 hover:text-white transition cursor-not-allowed">
          <i className="fas fa-search-plus text-xs" />
        </button>
      </div>
    </div>
  );
}
