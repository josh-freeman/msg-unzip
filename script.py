import os
import shutil
import logging as log

if __name__ == "__main__":
    current_dir = os.getcwd()
    log.basicConfig(level=log.INFO, format="%(asctime)s  - %(message)s")
    log.info(f"Current directory: {current_dir}")
    # first iterate recursively over all files in the current directory
    while True:
        no_zips = True
        for root, dirs, files in os.walk(current_dir):
            for file in files:
                if file.endswith(".zip"):
                    no_zips = False
                    log.info(f"Found zip file: {file}")
                    # extract the zip file
                    shutil.unpack_archive(os.path.join(root, file), root)
                    # remove the zip file
                    os.remove(os.path.join(root, file))
                    break

        if no_zips:
            log.info("No zip files found in the current directory")
            break
    
    # iterate again , again recursively, and look for directories of images called "pellets".
    for root, dirs, files in os.walk(current_dir):
        for dir in dirs:
            if dir == "pellets":
                log.info(f"Found directory of images: {dir}")
                # the directory will contain folders of images.
                # the name of a folder is a label for the images inside it.
                # two pellet directories in different locations can contain folders with the same name.
                # for each subdirectory subdir in dir, move its contents up to current_dir/pellets/subdir.
                # if the subdir already exists in current_dir, merge the contents of the two directories.
                # if it does not exist yet, create it.
                # if a file with the same name exists in both directories, log a warning and overwrite the file in current_dir/pellets/subdir
                for subdir in [d for d in os.listdir(os.path.join(root, dir)) if os.path.isdir(os.path.join(root, dir, d))]:
                    log.info(f"Found subdirectory of images: {subdir}")
                    if not os.path.exists(os.path.join(current_dir, "pellets", subdir)):
                        os.makedirs(os.path.join(current_dir, "pellets", subdir))
                    for file in os.listdir(os.path.join(root, dir, subdir)):
                        if os.path.exists(os.path.join(current_dir, "pellets", subdir, file)):
                            log.warning(f"File {file} already exists in {os.path.join(current_dir, 'pellets', subdir)}")
                        shutil.move(os.path.join(root, dir, subdir, file), os.path.join(current_dir, "pellets", subdir, file))

    log.info("Finished processing")

    #remove all empty directories, i.e. directories that do not contain any files at any level (they may contain other directories)
    for root, dirs, files in os.walk(current_dir):
        for dir in dirs:
            if not os.listdir(os.path.join(root, dir)):
                os.rmdir(os.path.join(root, dir))
                

    # do a final check for duplicates
    for root, dirs, files in os.walk(os.path.join(current_dir, "pellets")):
        for file in files:
            if os.path.exists(os.path.join(current_dir, "pellets", file)):
                log.warning(f"File {file} already exists in {os.path.join(current_dir, 'pellets')}")
                os.remove(os.path.join(root, file))