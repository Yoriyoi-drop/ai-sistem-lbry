package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

// ScanRequest represents a request to perform a security scan
type ScanRequest struct {
	Name        string                 `json:"name"`
	ScanType    string                 `json:"scan_type"`
	Target      string                 `json:"target"`
	Parameters  map[string]interface{} `json:"parameters,omitempty"`
}

// ScanResult represents the result of a security scan
type ScanResult struct {
	ID          string      `json:"id"`
	Name        string      `json:"name"`
	Status      string      `json:"status"`
	Target      string      `json:"target"`
	Findings    []Finding   `json:"findings"`
	StartTime   time.Time   `json:"start_time"`
	EndTime     time.Time   `json:"end_time"`
	Severity    string      `json:"severity"`
	Description string      `json:"description"`
}

// Finding represents a security vulnerability or issue found during scanning
type Finding struct {
	ID          string `json:"id"`
	Type        string `json:"type"`
	Severity    string `json:"severity"`
	Description string `json:"description"`
	Location    string `json:"location"`
	Payload     string `json:"payload"`
	Recommendation string `json:"recommendation"`
}

// Scanner represents the main scanner service
type Scanner struct {
	scans map[string]ScanResult
}

// NewScanner creates a new scanner instance
func NewScanner() *Scanner {
	return &Scanner{
		scans: make(map[string]ScanResult),
	}
}

// StartScan initiates a new security scan
func (s *Scanner) StartScan(w http.ResponseWriter, r *http.Request) {
	var req ScanRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	// Generate a unique ID for the scan
	scanID := fmt.Sprintf("scan_%d", time.Now().Unix())

	// Create a new scan result
	scanResult := ScanResult{
		ID:        scanID,
		Name:      req.Name,
		Status:    "running",
		Target:    req.Target,
		StartTime: time.Now(),
		EndTime:   time.Time{}, // Will be set when scan completes
		Severity:  "pending",
		Description: fmt.Sprintf("Scan of %s in progress", req.Target),
	}

	// Store the scan
	s.scans[scanID] = scanResult

	// In a real implementation, we would start the actual scan in a goroutine
	// Here we'll simulate by completing the scan immediately
	go s.completeScan(scanID, req)

	// Return the scan ID
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"scan_id": scanID})
}

// completeScan simulates completing a scan with findings
func (s *Scanner) completeScan(scanID string, req ScanRequest) {
	time.Sleep(2 * time.Second) // Simulate scan time

	// Create simulated findings based on scan type
	findings := s.generateFindings(req.ScanType, req.Target)

	// Update the scan result
	scanResult := ScanResult{
		ID:        scanID,
		Name:      req.Name,
		Status:    "completed",
		Target:    req.Target,
		Findings:  findings,
		StartTime: time.Now().Add(-2 * time.Second),
		EndTime:   time.Now(),
		Severity:  s.calculateSeverity(findings),
		Description: fmt.Sprintf("Scan of %s completed with %d findings", req.Target, len(findings)),
	}

	// Update the stored scan
	s.scans[scanID] = scanResult
}

// generateFindings creates simulated findings based on the scan type
func (s *Scanner) generateFindings(scanType, target string) []Finding {
	var findings []Finding

	// Generate some common findings based on scan type
	switch scanType {
	case "vulnerability":
		findings = append(findings, Finding{
			ID:          fmt.Sprintf("vuln_%d", time.Now().Unix()),
			Type:        "SQL Injection",
			Severity:    "High",
			Description: "SQL injection vulnerability detected",
			Location:    fmt.Sprintf("%s/login", target),
			Payload:     "' OR '1'='1",
			Recommendation: "Use parameterized queries and input validation",
		})
		findings = append(findings, Finding{
			ID:          fmt.Sprintf("vuln_%d", time.Now().Unix()),
			Type:        "Cross-Site Scripting",
			Severity:    "Medium",
			Description: "XSS vulnerability detected",
			Location:    fmt.Sprintf("%s/search", target),
			Payload:     "<script>alert(1)</script>",
			Recommendation: "Implement proper output encoding and input validation",
		})
	case "compliance":
		findings = append(findings, Finding{
			ID:          fmt.Sprintf("comp_%d", time.Now().Unix()),
			Type:        "Data Exposure",
			Severity:    "High",
			Description: "Sensitive data exposed in response",
			Location:    fmt.Sprintf("%s/api/users", target),
			Payload:     "password, ssn, credit_card",
			Recommendation: "Implement data masking and access controls",
		})
	case "penetration":
		findings = append(findings, Finding{
			ID:          fmt.Sprintf("pent_%d", time.Now().Unix()),
			Type:        "Open Port",
			Severity:    "Low",
			Description: "Unsecured port detected",
			Location:    fmt.Sprintf("%s:22", target),
			Payload:     "SSH service running with default credentials",
			Recommendation: "Disable unnecessary services and secure with strong authentication",
		})
	default:
		// Default findings
		findings = append(findings, Finding{
			ID:          fmt.Sprintf("gen_%d", time.Now().Unix()),
			Type:        "Information Disclosure",
			Severity:    "Low",
			Description: "Version information disclosed",
			Location:    target,
			Payload:     "Server: nginx/1.18.0",
			Recommendation: "Remove version headers from responses",
		})
	}

	return findings
}

// calculateSeverity determines the overall severity based on findings
func (s *Scanner) calculateSeverity(findings []Finding) string {
	highCount := 0
	mediumCount := 0

	for _, finding := range findings {
		switch finding.Severity {
		case "Critical", "High":
			highCount++
		case "Medium":
			mediumCount++
		}
	}

	if highCount > 0 {
		return "High"
	} else if mediumCount > 0 {
		return "Medium"
	}
	return "Low"
}

// GetScan retrieves the status of a specific scan
func (s *Scanner) GetScan(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	scanID := vars["id"]

	scan, exists := s.scans[scanID]
	if !exists {
		http.Error(w, "Scan not found", http.StatusNotFound)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(scan)
}

// ListScans retrieves all scans
func (s *Scanner) ListScans(w http.ResponseWriter, r *http.Request) {
	var scans []ScanResult
	for _, scan := range s.scans {
		scans = append(scans, scan)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(scans)
}

// HealthCheck provides a health check endpoint
func (s *Scanner) HealthCheck(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{
		"status":    "healthy",
		"service":   "security-scanner",
		"timestamp": time.Now().Format(time.RFC3339),
	})
}

func main() {
	scanner := NewScanner()
	
	// Create a new router
	r := mux.NewRouter()
	
	// Define API routes
	r.HandleFunc("/scan", scanner.StartScan).Methods("POST")
	r.HandleFunc("/scan/{id}", scanner.GetScan).Methods("GET")
	r.HandleFunc("/scans", scanner.ListScans).Methods("GET")
	r.HandleFunc("/health", scanner.HealthCheck).Methods("GET")
	
	// Print startup message
	fmt.Println("🚀 Infinite AI Security Scanner starting...")
	fmt.Println("📡 Listening on :8080")
	
	// Start the server
	log.Fatal(http.ListenAndServe(":8080", r))
}