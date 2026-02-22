// // // import jsPDF from "jspdf";

// // // export function exportSessionToPDF(session) {
// // //   const doc = new jsPDF();
// // //   let y = 10;

// // //   doc.setFontSize(16);
// // //   doc.text("SmartDocs AI – Chat Session", 10, y);
// // //   y += 10;

// // //   doc.setFontSize(10);
// // //   doc.text(`Session ID: ${session.session_id}`, 10, y);
// // //   y += 6;

// // //   doc.text(
// // //     `Created: ${new Date(session.created_at).toLocaleString()}`,
// // //     10,
// // //     y
// // //   );
// // //   y += 10;

// // //   doc.line(10, y, 200, y);
// // //   y += 10;

// // //   let qCount = 1;

// // //   for (let i = 0; i < session.history.length; i++) {
// // //     const msg = session.history[i];

// // //     // USER QUESTION
// // //     if (msg.role === "user") {
// // //       if (y > 270) {
// // //         doc.addPage();
// // //         y = 10;
// // //       }

// // //       doc.setFontSize(12);
// // //       doc.text(`Q${qCount}: ${msg.text}`, 10, y, {
// // //         maxWidth: 180,
// // //       });
// // //       y += 8;

// // //       // NEXT MESSAGE = AI ANSWER
// // //       const next = session.history[i + 1];
// // //       if (next && next.role === "assistant") {
// // //         doc.setFontSize(11);
// // //         doc.text(`A: ${next.text}`, 10, y, {
// // //           maxWidth: 180,
// // //         });
// // //         y += 10;

// // //         // Citations
// // //         if (next.citations?.length) {
// // //           doc.setFontSize(9);
// // //           next.citations.forEach((c) => {
// // //             doc.text(
// // //               `• ${c.source_file} (Page ${c.page_number})`,
// // //               12,
// // //               y
// // //             );
// // //             y += 5;
// // //           });
// // //         }

// // //         y += 6;
// // //         qCount++;
// // //       }
// // //     }
// // //   }

// // //   doc.save(`smartdocs_session_${session.session_id}.pdf`);
// // // }

// // import { jsPDF } from "jspdf";
// // import autoTable from "jspdf-autotable"; // Import the function directly

// // export const exportSessionToPDF = (sessionData) => {
// //   const session = sessionData?.data ? sessionData.data : sessionData;
// //   const history = session?.history;

// //   if (!history || !Array.isArray(history)) {
// //     alert("This session contains no chat history to export.");
// //     return;
// //   }

// //   try {
// //     const doc = new jsPDF();
    
// //     // Header
// //     doc.setFontSize(18);
// //     doc.setTextColor(37, 99, 235);
// //     doc.text("SmartDocs AI - Chat Export", 14, 20);

// //     doc.setFontSize(10);
// //     doc.setTextColor(100);
// //     doc.text(`User: ${session.user || 'User'}`, 14, 30);
// //     doc.text(`Session: ${session.title || 'Untitled'}`, 14, 35);
// //     doc.text(`Date: ${new Date().toLocaleString()}`, 14, 40);

// //     // Prepare data
// //     const rows = history.map(m => [
// //       m.role === "user" ? "User" : "SmartDocs AI",
// //       m.text
// //     ]);

// //     // ✅ CALL AUTOTABLE CORRECTLY
// //     autoTable(doc, {
// //       startY: 50,
// //       head: [['Role', 'Content']],
// //       body: rows,
// //       theme: 'striped',
// //       headStyles: { fillColor: [37, 99, 235] },
// //       styles: { fontSize: 9, cellPadding: 4, overflow: 'linebreak' },
// //       columnStyles: { 0: { fontStyle: 'bold', cellWidth: 30 } }
// //     });

// //     doc.save(`SmartDocs_${session.session_id || 'export'}.pdf`);
// //   } catch (err) {
// //     console.error("PDF Generation Failed:", err);
// //     alert("Could not generate PDF. Check console for details.");
// //   }
// // };

// import { jsPDF } from "jspdf";
// import autoTable from "jspdf-autotable";

// export function exportSessionToPDF(session) {
//   if (!session || !Array.isArray(session.history)) {
//     alert("No chat history found in this session.");
//     return;
//   }

//   const doc = new jsPDF();
//   let y = 20;

//   /* ================= HEADER ================= */
//   doc.setFontSize(18);
//   doc.setTextColor(37, 99, 235); // Blue-600
//   doc.text("SmartDocs AI — Chat Session", 14, y);

//   y += 8;
//   doc.setFontSize(10);
//   doc.setTextColor(100);

//   doc.text(`Session ID: ${session.session_id}`, 14, y);
//   y += 5;
//   doc.text(
//     `Created: ${new Date(session.created_at).toLocaleString()}`,
//     14,
//     y
//   );

//   y += 10;

//   /* ================= BUILD Q/A ROWS ================= */
//   const rows = [];
  
//   session.history.forEach((chat, index) => {
//     // 1. Add User Question
//     rows.push([
//       `Q${index + 1}`,
//       chat.question || "No question text"
//     ]);

//     // 2. Add AI Answer
//     rows.push([
//       "Answer",
//       chat.answer || "No response text"
//     ]);

//     // 3. Add Citations if they exist
//     if (chat.citations && chat.citations.length > 0) {
//       chat.citations.forEach((c) => {
//         rows.push([
//           "Source",
//           `${c.source_file} (Page ${c.page_number})`
//         ]);
//       });
//     }
//   });

//   /* ================= TABLE ================= */
//   autoTable(doc, {
//     startY: y,
//     head: [["Type", "Content"]],
//     body: rows,
//     theme: "striped",
//     headStyles: {
//       fillColor: [37, 99, 235],
//       textColor: 255,
//       fontStyle: "bold",
//     },
//     styles: {
//       fontSize: 9,
//       cellPadding: 4,
//       overflow: "linebreak",
//     },
//     columnStyles: {
//       0: { cellWidth: 25, fontStyle: "bold" },
//       1: { cellWidth: 155 },
//     },
//     // Optional: Add spacing between Q/A pairs
//     didParseCell: function (data) {
//       if (data.section === 'body' && data.column.index === 0) {
//         if (data.cell.raw.startsWith('Q')) {
//           data.cell.styles.textColor = [37, 99, 235];
//         }
//       }
//     }
//   });

//   /* ================= SAVE ================= */
//   doc.save(`SmartDocs_Session_${session.session_id}.pdf`);
// }

import { jsPDF } from "jspdf";
import autoTable from "jspdf-autotable";

export function exportSessionToPDF(session) {
  // 1. Validation
  if (!session || !Array.isArray(session.history)) {
    alert("No chat history found in this session.");
    return;
  }

  try {
    const doc = new jsPDF();
    let y = 20;

    /* ================= HEADER ================= */
    doc.setFontSize(18);
    doc.setTextColor(37, 99, 235); // Blue-600
    doc.text("SmartDocs AI — Chat Session", 14, y);

    y += 8;
    doc.setFontSize(10);
    doc.setTextColor(100);

    doc.text(`Session ID: ${session.session_id}`, 14, y);
    y += 5;
    doc.text(
      `Created: ${new Date(session.created_at).toLocaleString()}`,
      14,
      y
    );

    y += 10;

    /* ================= BUILD ROWS ================= */
    // Since history is [ {role: "user", content: "..."}, {role: "assistant", content: "..."} ]
    const rows = [];
    
    session.history.forEach((msg) => {
      const isUser = msg.role === "user";
      
      // Add the main message
      rows.push([
        isUser ? "USER" : "AI",
        msg.content || msg.text || ""
      ]);

      // If it's an AI message with citations, add them as sub-rows
      if (!isUser && msg.citations && msg.citations.length > 0) {
        msg.citations.forEach((c) => {
          rows.push([
            "SOURCE",
            `${c.source_file} (Page ${c.page_number})`
          ]);
        });
      }
    });

    /* ================= GENERATE TABLE ================= */
    // We use the imported 'autoTable' function directly to avoid "doc.autoTable" errors
    autoTable(doc, {
      startY: y,
      head: [["Role", "Content"]],
      body: rows,
      theme: "grid",
      headStyles: {
        fillColor: [37, 99, 235],
        textColor: 255,
        fontStyle: "bold",
      },
      styles: {
        fontSize: 9,
        cellPadding: 4,
        overflow: "linebreak",
      },
      columnStyles: {
        0: { cellWidth: 25, fontStyle: "bold" },
        1: { cellWidth: "auto" },
      },
      didParseCell: function (data) {
        // Style "USER" and "AI" labels differently
        if (data.section === 'body' && data.column.index === 0) {
          if (data.cell.raw === 'USER') {
            data.cell.styles.textColor = [37, 99, 235];
          }
          if (data.cell.raw === 'SOURCE') {
            data.cell.styles.fontStyle = 'italic';
            data.cell.styles.textColor = [100, 100, 100];
          }
        }
      }
    });

    /* ================= SAVE ================= */
    doc.save(`SmartDocs_Export_${session.session_id}.pdf`);
    
  } catch (error) {
    console.error("PDF Export Error:", error);
    alert("Error generating PDF. Please check the console.");
  }
}