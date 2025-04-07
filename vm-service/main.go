package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"path/filepath"
	"sync"
	"time"

	"github.com/google/uuid"
)

type VMCreateRequest struct {
	Image     string      `json:"image"`
	Name      string      `json:"name"`
	Ports     [][2]int    `json:"ports"`
	Resources VMResources `json:"resources"`
}

type VMResources struct {
	CPU    int `json:"cpu"`
	Memory int `json:"memory"`
}

type VMDeleteRequest struct {
	UUID string `json:"uuid"`
}

var (
	mutex      sync.Mutex
	storageDir = "./data"
)

func createVMHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req VMCreateRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	vmID := uuid.New().String()
	filePath := filepath.Join(storageDir, vmID+".json")

	vmData, err := json.Marshal(req)
	if err != nil {
		http.Error(w, "Error creating VM", http.StatusInternalServerError)
		return
	}

	mutex.Lock()
	defer mutex.Unlock()

	if err := ioutil.WriteFile(filePath, vmData, 0644); err != nil {
		http.Error(w, "Error saving VM data", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusCreated)
	fmt.Fprintf(w, "VM created with ID: %s\n", vmID)
}

func deleteVMHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodDelete {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Parse a single UUID from the request body
	var req VMDeleteRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	filePath := filepath.Join(storageDir, req.UUID+".json")

	mutex.Lock()
	defer mutex.Unlock()

	// Attempt to delete the single file
	if err := os.Remove(filePath); err != nil {
		if os.IsNotExist(err) {
			http.Error(w, fmt.Sprintf("VM %s not found", req.UUID), http.StatusNotFound)
			return
		}
		http.Error(w, fmt.Sprintf("Error deleting VM %s: %v", req.UUID, err), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "VM %s deleted successfully\n", req.UUID)
}

func main() {
	// Ensure the storage directory exists
	if err := os.MkdirAll(storageDir, 0755); err != nil {
		panic(fmt.Sprintf("Failed to create storage directory: %v", err))
	}

	mux := http.NewServeMux()
	mux.HandleFunc("/create", createVMHandler)
	mux.HandleFunc("/delete", deleteVMHandler)

	server := &http.Server{
		Addr:           ":8080",
		Handler:        mux,
		ReadTimeout:    5 * time.Second,
		WriteTimeout:   10 * time.Second,
		MaxHeaderBytes: 1 << 20,
	}

	fmt.Println("Starting server on :8080...")
	if err := server.ListenAndServe(); err != nil {
		panic(fmt.Sprintf("Failed to start server: %v", err))
	}
}
